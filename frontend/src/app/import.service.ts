import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { of, throwError } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

interface IImportResponse {
  flag: 0 | 1;
}

@Injectable({
  providedIn: 'root',
})
export class ImportService {
  constructor(private http: HttpClient) {}

  importAll() {
    return this.http
      .post<IImportResponse>(`${environment.apiUrl}/import`, {
        import_mode: 'auto',
      })
      .pipe(
        switchMap((response) =>
          response.flag === 1 ? of(response) : throwError('Error')
        )
      );
  }

  import(id: number) {
    return this.http
      .post<IImportResponse>(`${environment.apiUrl}/import`, {
        import_mode: 'manual',
        atel_num: id,
      })
      .pipe(
        switchMap((response) =>
          response.flag === 1 ? of(response) : throwError('Error')
        )
      );
  }
}
