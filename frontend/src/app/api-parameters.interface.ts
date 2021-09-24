import { Match } from './match.enum';

export interface ApiParameters {
  term: string;
  search_mode: string;
  search_data: string | string[];
  keyword_mode: Match;
  keywords?: string[];
  start_date?: string;
  end_date?: string;
}
