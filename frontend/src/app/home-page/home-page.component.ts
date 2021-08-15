import { Component, OnInit } from '@angular/core';

enum SearchMode {
  Name,
  Coordinate,
}

enum Match {
  Any = 'any',
  All = 'all',
  None = 'none',
}

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  public SearchMode = SearchMode;
  public Match = Match;

  public keywords = '';
  public mode = SearchMode.Name;
  public name = '';
  public ra = '';
  public decimals = '';
  public radius = '';
  public match = Match.Any;

  constructor() {}

  ngOnInit(): void {}

  search() {}
}
