import { Component, ElementRef, ViewChild } from '@angular/core';
import { Parameters } from '../parameters.interface';
import { SearchResultsComponent } from '../search-results/search-results.component';
import { SearchService } from '../search.service';
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

  constructor(private searchService: SearchService) {}

  search(parameters: Parameters) {
    console.log(parameters);

    this.searchService.search(parameters).subscribe((telegrams) => {
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
    });

    this.results?.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }
}
