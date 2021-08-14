import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private _token?: string;

  public get token() {
    return this._token;
  }

  constructor(private http: HttpClient) {}

  authenticate(username: string, password: string) {
    return this.http
      .post<string>(`${environment.apiUrl}/authenticate`, {
        username,
        password,
      })
      .pipe(tap((token) => (this._token = token)));
  }
}
