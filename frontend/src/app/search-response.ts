import { ApiTelegram } from './api-telegram.interface';
import { Node, Link } from './network-graph/network-graph.component';

export interface SearchResponse {
  report_list: ApiTelegram[];
  node_list: Node[];
  edge_list: Link[];
}
