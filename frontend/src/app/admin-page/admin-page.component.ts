import {
  HttpClient,
  HttpErrorResponse,
  HttpStatusCode,
} from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { AuthenticationService } from '../authentication.service';
import { ErrorUtilities } from '../error-utilities';
import { ImportService } from '../import.service';
import { Metadata } from '../metadata.interface';

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.scss'],
})
export class AdminPageComponent implements OnInit {
  public id = 0;

  public upcoming?: number;

  public loadingAuto = false;
  public loadingManual = false;

  constructor(
    private http: HttpClient,
    private importService: ImportService,
    private snackBar: MatSnackBar,
    private authenticationService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit() {
    this.fetchMetadata();
  }

  importAll() {
    return this.importService.importAll().pipe(
      ErrorUtilities.handleHttpResponse('Failed to import ATels'),
      tap(() =>
        this.snackBar.open('Started importing ATels', 'Close', {
          duration: 8000,
        })
      ),
      catchError((error) => {
        if (
          error instanceof HttpErrorResponse &&
          error.status === HttpStatusCode.Unauthorized
        ) {
          this.authenticationService.invalidate();
          return this.router.navigate(['/authenticate']);
        }

        this.snackBar.open(error.message, 'Close', {
          duration: 8000,
        });

        return throwError(error);
      })
    );
  }

  import() {
    return this.importService.import(this.id).pipe(
      ErrorUtilities.handleHttpResponse('Failed to import ATel'),
      tap(() =>
        this.snackBar.open('ATel successfully imported', 'Close', {
          duration: 8000,
        })
      ),
      catchError((error) => {
        if (
          error instanceof HttpErrorResponse &&
          error.status === HttpStatusCode.Unauthorized
        ) {
          this.authenticationService.invalidate();
          return this.router.navigate(['/authenticate']);
        }

        this.snackBar.open(error.message, 'Close', {
          duration: 8000,
        });

        return throwError(error);
      })
    );
  }

  fetchMetadata() {
    this.http
      .get<Metadata>(`${environment.apiUrl}/metadata`)
      .subscribe((metadata) => {
        this.upcoming = metadata.nextAtel;
      });
  }
}
