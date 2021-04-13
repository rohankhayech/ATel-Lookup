import { Component } from '@angular/core';
import { dxEvent } from 'devextreme/events';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass'],
})
export class AppComponent {
  object: 'asteroid' | 'star' | 'planet' = 'asteroid';

  radio = false;
  millimeter = false;
  optical = false;

  keywords = '';

  dataSource = [
    {
      day: 'Monday',
      oranges: 3,
    },
    {
      day: 'Tuesday',
      oranges: 2,
    },
    {
      day: 'Wednesday',
      oranges: 3,
    },
    {
      day: 'Thursday',
      oranges: 4,
    },
    {
      day: 'Friday',
      oranges: 6,
    },
    {
      day: 'Saturday',
      oranges: 11,
    },
    {
      day: 'Sunday',
      oranges: 4,
    },
  ];

  handlePointClick(e: any) {
    console.log(e);
  }

  handleSeriesClick(e: any) {
    console.log(e);
  }
}
