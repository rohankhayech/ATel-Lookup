import { Component, Input } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-telegram-card',
  templateUrl: './telegram-card.component.html',
  styleUrls: ['./telegram-card.component.scss'],
})
export class TelegramCardComponent {
  @Input() public telegram?: Telegram;

  public get url() {
    return `${environment.astronomersTelegramUrl}/?read=${this.telegram?.id}`;
  }

  visit() {
    window.open(this.url, '_blank');
  }
}
