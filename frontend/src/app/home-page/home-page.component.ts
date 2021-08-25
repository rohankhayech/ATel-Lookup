import { Component, ElementRef, ViewChild } from '@angular/core';
import { SearchResultsComponent } from '../search-results/search-results.component';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent {
  @ViewChild(SearchResultsComponent, { read: ElementRef })
  public results?: ElementRef;

  public telegrams?: Telegram[];

  constructor() {}

  search(payload: unknown) {
    console.log(payload);

    this.telegrams = [
      {
        id: 1,
        title: 'Apple',
        date: new Date(),
        authors: ['A', 'B', 'C'],
        keywords: ['A', 'B', 'C'],
      },
      {
        id: 2,
        title: 'Banana',
        date: new Date(),
        authors: ['A', 'B', 'C'],
        keywords: ['A', 'B', 'C'],
      },
      {
        id: 3,
        title: 'Citrus',
        date: new Date(),
        authors: ['A', 'B', 'C'],
        keywords: ['A', 'B', 'C'],
      },
    ];

    this.results?.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }
}
