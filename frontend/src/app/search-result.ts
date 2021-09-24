import { Telegram } from './telegram.interface';
import { Node, Link } from './network-graph/network-graph.component';

export interface SearchResult {
  telegrams: Telegram[];
  nodes: Node[];
  links: Link[];
}
