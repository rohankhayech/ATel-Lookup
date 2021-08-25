import { Component, Input, OnInit } from '@angular/core';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss'],
})
export class SearchResultsComponent implements OnInit {
  @Input() public telegrams?: Telegram[];

  constructor() {}

  ngOnInit(): void {}
}
