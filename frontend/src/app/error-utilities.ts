import { of, throwError } from 'rxjs';
import { switchMap } from 'rxjs/operators';

export interface IHttpResponse {
  flag: 0 | 1 | 2;
  msg: string;
}

export class ErrorUtilities {
  public static handleHttpResponse<T extends IHttpResponse>(message: string) {
    return switchMap((response: T) => {
      switch (response.flag) {
        case 0: // system error
          return throwError(new Error(message));
        case 1: // success
          return of(response);
        case 2: // user error
          return throwError(new Error(response.msg));
        default:
          // unexpected error
          return throwError(new Error(message));
      }
    });
  }
}
