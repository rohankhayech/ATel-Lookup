import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { finalize } from 'rxjs/operators';
import { ImportService } from '../import.service';

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.scss'],
})
export class AdminPageComponent {
  public id = 0;

  public loadingAuto = false;
  public loadingManual = false;

  constructor(
    private importService: ImportService,
    private snackBar: MatSnackBar
  ) {}

  importAll() {
    this.loadingAuto = true;

    this.importService
      .importAll()
      .pipe(finalize(() => (this.loadingAuto = false)))
      .subscribe(() =>
        this.snackBar.open('ATels successfully imported', 'Close', {
          duration: 8000,
        })
      );
  }

  import() {
    this.loadingManual = true;

    this.importService
      .import(this.id)
      .pipe(finalize(() => (this.loadingManual = false)))
      .subscribe(() =>
        this.snackBar.open('ATel successfully imported', 'Close', {
          duration: 8000,
        })
      );
  }
}
