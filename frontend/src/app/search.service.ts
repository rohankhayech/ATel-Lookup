import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Parameters } from './parameters.interface';
import { SearchMode } from './search-mode.enum';
import { ApiParameters } from './api-parameters.interface';
import { Telegram } from './telegram.interface';
import { ApiTelegram } from './api-telegram.interface';
import { switchMap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { SearchResponse } from './search-response';
import { Moment } from 'moment';
import { SearchResult } from './search-result';
import { Link } from './network-graph/network-graph.component';
import { ErrorUtilities } from './error-utilities';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  constructor(private http: HttpClient) {}

  search(parameters: Parameters) {
    const params = this.serializeParameters(parameters);
    return this.http
      .post<SearchResponse>(`${environment.apiUrl}/search`, {
        ...params,
      })
      .pipe(
        ErrorUtilities.handleHttpResponse('Search failed'),
        switchMap((response): Observable<SearchResult> => {
          const telegrams = response.report_list.map(this.deserializeTelegram);
          const nodes = telegrams.filter((telegram) =>
            response.node_list.includes(telegram.id)
          );
          const links = response.edge_list
            .map(this.deserializeLink)
            .filter((link) => this.existingNodeFilter(nodes, link));
          return of({ telegrams, nodes, links });
        })
      );
  }

  serializeParameters(parameters: Parameters): ApiParameters {
    return {
      term: parameters.query,
      search_mode: parameters.mode === SearchMode.Name ? 'name' : 'coords',
      search_data:
        parameters.mode === SearchMode.Name
          ? parameters.name
          : [
              parameters.coordinates.ra,
              parameters.coordinates.declination,
              parameters.coordinates.radius,
            ],
      keyword_mode: parameters.match,
      keywords: parameters.keywords,
      start_date: this.serializeDate(parameters.start),
      end_date: this.serializeDate(parameters.end),
    };
  }

  serializeDate(date?: Moment) {
    return date?.format('YYYY-MM-DD');
  }

  deserializeTelegram(telegram: ApiTelegram): Telegram {
    return {
      id: telegram.atel_num,
      title: telegram.title,
      date: new Date(telegram.submission_date),
      authors: telegram.authors,
      body: telegram.body,
      referenced: telegram.referenced_reports,
    };
  }

  deserializeLink(link: number[]) {
    return {
      source: link[0],
      target: link[1],
    };
  }

  existingNodeFilter(nodes: Telegram[], link: Link) {
    // ensure both source and target are in nodes list
    return (
      nodes.some((j) => j.id === link.source) &&
      nodes.some((j) => j.id === link.target)
    );
  }

  pad(n: number) {
    return n.toString().padStart(2, '0');
  }
}
