import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Parameters } from './parameters.interface';
import { Telegram } from './telegram.interface';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  constructor(private http: HttpClient) {}

  search(parameters: Parameters) {
    const params = this.serializeParameters(parameters);
    return this.http.get<Telegram[]>(`${environment.apiUrl}/search`, {
      params,
    });
  }

  serializeParameters(parameters: Parameters) {
    return parameters as any;
  }
}
