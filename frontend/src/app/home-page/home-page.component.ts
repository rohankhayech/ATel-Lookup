import { Component, ElementRef, ViewChild } from '@angular/core';
import { SearchResultsComponent } from '../search-results/search-results.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent {
  @ViewChild(SearchResultsComponent, { read: ElementRef })
  public searchResults?: ElementRef;

  constructor() {}

  search(payload: unknown) {
    console.log(payload);

    this.searchResults?.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }
}
