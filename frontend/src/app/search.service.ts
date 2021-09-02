import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Parameters } from './parameters.interface';
import { SearchMode } from './search-mode.enum';
import { ApiParameters } from './api-parameters.interface';
import { Telegram } from './telegram.interface';
import { ApiTelegram } from './api-telegram.interface';
import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';
import { SearchResponse } from './search-response';
import { Moment } from 'moment';

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
        switchMap((response) =>
          of(response.report_list.map(this.deserializeTelegram))
        )
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
              parameters.coordinates.declination,
              parameters.coordinates.ra,
              parameters.coordinates.radius,
            ],
      keyword_mode: parameters.match,
      keywords: parameters.keywords,
      start_date: this.serializeDate(parameters.start),
      end_date: this.serializeDate(parameters.end),
    };
  }

  serializeDate(date?: Moment) {
    return date?.format('DD/MM/YYYY');
  }

  deserializeTelegram(telegram: ApiTelegram): Telegram {
    return {
      id: telegram.atel_num,
      title: telegram.title,
      date: telegram.submission_date,
      authors: telegram.authors,
      body: telegram.body,
      referenced: telegram.referenced_reports,
    };
  }

  pad(n: number) {
    return n.toString().padStart(2, '0');
  }
}
