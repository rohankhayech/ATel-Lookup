import {
  Component,
  HostListener,
  Input,
  OnChanges,
  OnInit,
} from '@angular/core';
import { fromEvent } from 'rxjs';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit, OnChanges {
  @Input() public telegrams: Telegram[] | undefined = [];

  constructor() {
    const resize$ = fromEvent(window, 'resize');
    resize$.subscribe(() => this.drawChart());
  }

  ngOnInit() {
    google.charts.load('current', { packages: ['timeline'] });
    google.charts.setOnLoadCallback(() => this.drawChart());
  }

  ngOnChanges() {
    this.drawChart();
  }

  private drawChart() {
    var container = document.getElementById('timeline') as Element;
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    const rows = [];
    for (const telegram of this.telegrams ?? []) {
      const tooltip = `<b>${telegram.title}</b><p>${
        telegram.authors
      }</p><p>${telegram.date.toLocaleDateString()}</p>`;

      rows.push([
        'Report',
        telegram.authors,
        tooltip,
        telegram.date,
        telegram.date,
      ]);
    }

    dataTable.addColumn({ type: 'string', id: 'Type' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'string', role: 'tooltip' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows(rows);

    var options = {
      timeline: { groupByRowLabel: true },
    };

    chart.draw(dataTable, options);
  }
}
