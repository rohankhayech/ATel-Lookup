import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
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
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  public SearchMode = SearchMode;
  public Match = Match;

  public metadata?: Metadata;

  public query = '';
  public mode = SearchMode.Name;
  public name = '';
  public ra = '';
  public decimals = '';
  public radius = '';
  public match = Match.Any;
  public keywords: Keywords = {};

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

  search() {
    const keywords = this.metadata?.keywords.filter(
      (keyword) => this.keywords[keyword]
    );

    const coordinates = {
      ra: this.ra,
      decimals: this.decimals,
      radius: this.radius,
    };

    const data = {
      query: this.query,
      mode: this.mode,
      name: this.name,
      coordinates,
      match: this.match,
      keywords,
    };
  }
}
