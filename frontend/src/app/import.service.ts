import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ImportService {
  constructor(private http: HttpClient) {}

  importAll() {
    return this.http.post<void>(`${environment.apiUrl}/import`, {
      import_mode: 'auto',
    });
  }

  import(id: number) {
    return this.http.post<void>(`${environment.apiUrl}/import`, {
      import_mode: 'manual',
      atel_num: id,
    });
  }
}
