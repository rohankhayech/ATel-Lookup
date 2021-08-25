import { Component, Input } from '@angular/core';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss'],
})
export class SearchResultsComponent {
  @Input() public telegrams?: Telegram[];

  top() {
    window.scrollTo({ top: 0 });
  }
}
