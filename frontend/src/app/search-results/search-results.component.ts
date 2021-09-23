import { Component, Input, QueryList, ViewChildren } from '@angular/core';
import { SearchResult } from '../search-result';
import { TelegramCardComponent } from '../telegram-card/telegram-card.component';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss'],
})
export class SearchResultsComponent {
  @Input() public result?: SearchResult;

  @ViewChildren(TelegramCardComponent)
  cards?: QueryList<TelegramCardComponent>;

  public readonly pageSize = 10;

  public page = 0;

  get view() {
    const index = this.page * this.pageSize;
    return this.result?.telegrams?.slice(index, index + this.pageSize);
  }

  top() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  scrollToTelegram(id: number) {
    this.cards?.forEach((card) => {
      if (card.telegram?.id === id) {
        card.scroll();
      }
    });
  }

  updatePage(page: number) {
    this.page = page;
    this.cards?.first.scroll();
  }
}
