import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
} from '@angular/core';
import { fromEvent } from 'rxjs';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit, OnChanges {
  @Output() public selectionChange = new EventEmitter<number>();

  @Input() public telegrams: Telegram[] | undefined = [];

  private loaded = false;

  constructor() {
    const resize$ = fromEvent(window, 'resize');
    resize$.subscribe(() => this.drawChart());
  }

  ngOnInit() {
    google.charts.load('current', { packages: ['timeline'] });
    google.charts.setOnLoadCallback(() => this.initialiseChart());
  }

  ngOnChanges() {
    this.drawChart();
  }

  private initialiseChart() {
    this.loaded = true;
    this.drawChart();
  }

  private drawChart() {
    if (!this.loaded) {
      return;
    }

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
        telegram.id,
        telegram.authors,
        tooltip,
        telegram.date,
        telegram.date,
      ]);
    }

    dataTable.addColumn({ type: 'string', id: 'Type' });
    dataTable.addColumn({ type: 'number', role: 'id' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'string', role: 'tooltip' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows(rows);

    var options = {
      timeline: { groupByRowLabel: true },
    };

    google.visualization.events.addListener(chart, 'select', () => {
      const selection = chart.getSelection();
      const id = dataTable.getValue(selection[0].row!, 1);
      this.selectionChange.emit(id);
    });

    chart.draw(dataTable, options);
  }
}
