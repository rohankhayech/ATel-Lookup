import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { IHttpResponse } from './error-utilities';

interface IImportResponse extends IHttpResponse {}

@Injectable({
  providedIn: 'root',
})
export class ImportService {
  constructor(private http: HttpClient) {}

  importAll() {
    return this.http.post<IImportResponse>(`${environment.apiUrl}/import`, {
      import_mode: 'auto',
    });
  }

  import(id: number) {
    return this.http.post<IImportResponse>(`${environment.apiUrl}/import`, {
      import_mode: 'manual',
      atel_num: id,
    });
  }
}
