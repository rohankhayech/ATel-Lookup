import { Component } from '@angular/core';
import { ImportService } from '../import.service';

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.scss'],
})
export class AdminPageComponent {
  public id = 0;

  constructor(private importService: ImportService) {}

  importAll() {
    this.importService.importAll().subscribe();
  }

  import() {
    this.importService.import(this.id).subscribe();
  }
}
