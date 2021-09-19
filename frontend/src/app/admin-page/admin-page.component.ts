import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
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
    return this.importService.importAll().pipe(
      tap(() =>
        this.snackBar.open('ATels successfully imported', 'Close', {
          duration: 8000,
        })
      ),
      catchError((error) => {
        this.snackBar.open('Failed to import ATels', 'Close', {
          duration: 8000,
        });

        return throwError(error);
      })
    );
  }

  import() {
    return this.importService.import(this.id).pipe(
      tap(() =>
        this.snackBar.open('ATel successfully imported', 'Close', {
          duration: 8000,
        })
      ),
      catchError((error) => {
        this.snackBar.open('Failed to import ATel', 'Close', {
          duration: 8000,
        });

        return throwError(error);
      })
    );
  }
}
