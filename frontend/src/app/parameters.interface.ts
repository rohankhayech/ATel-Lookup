import { Coordinates } from './coordinates.interface';
import { Match } from './match.enum';
import { SearchMode } from './search-mode.enum';

export interface Parameters {
  query: string;
  mode: SearchMode;
  name: string;
  coordinates: Coordinates;
  match: Match;
  keywords?: string[];
  start?: Date;
  end?: Date;
}
