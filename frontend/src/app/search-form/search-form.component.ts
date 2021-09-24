import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Moment } from 'moment';
import { EMPTY } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Coordinates } from '../coordinates.interface';
import { Match } from '../match.enum';
import { Metadata } from '../metadata.interface';
import { Parameters } from '../parameters.interface';
import { SearchMode } from '../search-mode.enum';
import { SearchResult } from '../search-result';
import { SearchService } from '../search.service';

interface Keywords {
  [key: string]: boolean;
}

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss'],
})
export class SearchFormComponent implements OnInit {
  @Output() public search = new EventEmitter<SearchResult>();

  public SearchMode = SearchMode;
  public Match = Match;

  public metadata?: Metadata;

  public query = '';
  public mode = SearchMode.Name;
  public name = '';
  public ra = '';
  public declination = '';
  public radius = '';
  public match = Match.Any;
  public keywords: Keywords = {};
  public start?: Moment;
  public end?: Moment;

  constructor(
    private http: HttpClient,
    private searchService: SearchService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.fetchMetadata();
  }

  fetchMetadata() {
    this.http
      .get<Metadata>(`${environment.apiUrl}/metadata`)
      .subscribe((metadata) => {
        this.metadata = metadata;

        for (const keyword of this.metadata.keywords) {
          this.keywords[keyword] = false;
        }
      });
  }

  submit() {
    if (!this.valid) {
      this.snackBar.open(
        'You must input either a free-text search query, object name, coordinates or keywords',
        'Close',
        { duration: 8000 }
      );
      return EMPTY;
    }

    const coordinates: Coordinates = {
      ra: this.ra,
      declination: this.declination,
      radius: this.radius,
    };

    const parameters: Parameters = {
      query: this.query,
      mode: this.mode,
      name: this.name,
      coordinates,
      match: this.match,
      keywords: this.keywordList,
      start: this.start,
      end: this.end,
    };

    return this.searchService.search(parameters).pipe(
      tap((telegrams) => this.search.emit(telegrams)),
      tap(({ telegrams }) => {
        if (telegrams.length === 0) {
          this.snackBar.open('No ATels matched your query', 'Close', {
            duration: 8000,
          });
        }
      })
    );
  }

  get valid() {
    return (
      this.query ||
      this.keywordList?.length ||
      (this.mode === SearchMode.Coordinate
        ? this.ra && this.declination && this.radius
        : this.name)
    );
  }

  get keywordList() {
    return this.metadata?.keywords.filter((keyword) => this.keywords[keyword]);
  }
}
