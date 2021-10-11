import { Component, ElementRef, ViewChild } from '@angular/core';
import { SearchResult } from '../search-result';
import { SearchResultsComponent } from '../search-results/search-results.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent {
  @ViewChild(SearchResultsComponent, { read: ElementRef })
  public results?: ElementRef;

  public result?: SearchResult;

  search(result: SearchResult) {
    this.result = result;

    if (this.result.telegrams.length > 0) {
      this.results?.nativeElement.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
