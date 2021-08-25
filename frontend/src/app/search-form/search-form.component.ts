import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { environment } from 'src/environments/environment';

interface Metadata {
  keywords: string[];
  lastUpdated: string;
  reportCount: number;
}

enum SearchMode {
  Name,
  Coordinate,
}

enum Match {
  Any = 'any',
  All = 'all',
  None = 'none',
}

interface Keywords {
  [key: string]: boolean;
}

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss'],
})
export class SearchFormComponent implements OnInit {
  @Output() public search = new EventEmitter<unknown>();

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
  public start?: Date;
  public end?: Date;

  constructor(private http: HttpClient) {}

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
    const keywords = this.metadata?.keywords.filter(
      (keyword) => this.keywords[keyword]
    );

    const coordinates = {
      ra: this.ra,
      declination: this.declination,
      radius: this.radius,
    };

    const payload = {
      query: this.query,
      mode: this.mode,
      name: this.name,
      coordinates,
      match: this.match,
      keywords,
      start: this.start,
      end: this.end,
    };

    this.search.emit(payload);
  }
}
