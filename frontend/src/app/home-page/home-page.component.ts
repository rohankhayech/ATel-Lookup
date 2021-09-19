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

  search(telegrams: Telegram[]) {
    this.telegrams = telegrams;

    this.results?.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }
}
