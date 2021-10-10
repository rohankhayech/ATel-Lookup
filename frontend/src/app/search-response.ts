import { ApiTelegram } from './api-telegram.interface';
import { IHttpResponse } from './error-utilities';

export interface SearchResponse extends IHttpResponse {
  report_list: ApiTelegram[];
  node_list: number[];
  edge_list: number[][];
}
