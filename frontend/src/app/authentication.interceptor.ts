import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpHeaders,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthenticationService } from './authentication.service';

@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {
  constructor(private authenticationService: AuthenticationService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    if (this.authenticationService.token !== null) {
      const authenticatedRequest = request.clone({
        headers: new HttpHeaders({
          Authorization: `Bearer ${this.authenticationService.token}`,
        }),
      });

      return next.handle(authenticatedRequest);
    }

    return next.handle(request);
  }
}
