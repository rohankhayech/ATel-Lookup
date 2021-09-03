import { Component, Input } from '@angular/core';
import { SearchResult } from '../search-result';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss'],
})
export class SearchResultsComponent {
  @Input() public result?: SearchResult;

  top() {
    window.scrollTo({ top: 0 });
  }
}
