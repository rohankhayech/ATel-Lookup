import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { Moment } from 'moment';
import { environment } from 'src/environments/environment';
import { Coordinates } from '../coordinates.interface';
import { Match } from '../match.enum';
import { Metadata } from '../metadata.interface';
import { Parameters } from '../parameters.interface';
import { SearchMode } from '../search-mode.enum';

interface Keywords {
  [key: string]: boolean;
}

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss'],
})
export class SearchFormComponent implements OnInit {
  @Output() public search = new EventEmitter<Parameters>();

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

    const coordinates: Coordinates = {
      ra: +this.ra,
      declination: +this.declination,
      radius: +this.radius,
    };

    const parameters: Parameters = {
      query: this.query,
      mode: this.mode,
      name: this.name,
      coordinates,
      match: this.match,
      keywords,
      start: this.start,
      end: this.end,
    };

    this.search.emit(parameters);
  }
}
