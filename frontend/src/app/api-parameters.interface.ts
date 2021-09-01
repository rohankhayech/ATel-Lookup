import { Match } from './match.enum';

export interface ApiParameters {
  search_mode: string;
  search_data: string | number[];
  keyword_mode: Match;
  keywords?: string[];
  start_date?: string;
  end_date?: string;
}
