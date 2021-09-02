export interface Telegram {
  id: number;
  title: string;
  date: Date;
  authors: string;
  body: string;
  referenced: number[];
}
