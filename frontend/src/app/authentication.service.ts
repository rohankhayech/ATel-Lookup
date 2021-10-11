import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { tap } from 'rxjs/operators';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private static readonly TOKEN_KEY = 'token';

  public token$ = new BehaviorSubject(this.token);

  public get token() {
    return localStorage.getItem(AuthenticationService.TOKEN_KEY);
  }

  public set token(value: string | null) {
    this.token$.next(value);

    if (value !== null) {
      localStorage.setItem(AuthenticationService.TOKEN_KEY, value);
    } else {
      localStorage.removeItem(AuthenticationService.TOKEN_KEY);
    }
  }

  constructor(private http: HttpClient) {}

  authenticate(username: string, password: string) {
    return this.http
      .post<string>(`${environment.apiUrl}/authenticate`, {
        username,
        password,
      })
      .pipe(tap((token) => (this.token = token)));
  }

  invalidate() {
    this.token = null;
  }
}
