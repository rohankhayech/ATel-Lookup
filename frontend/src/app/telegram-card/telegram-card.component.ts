import { Component, ElementRef, Input } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-telegram-card',
  templateUrl: './telegram-card.component.html',
  styleUrls: ['./telegram-card.component.scss'],
})
export class TelegramCardComponent {
  @Input() public telegram?: Telegram;

  constructor(private elementRef: ElementRef) {}

  public get url() {
    return `${environment.astronomersTelegramUrl}/?read=${this.telegram?.id}`;
  }

  scroll() {
    this.elementRef.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }

  visit() {
    window.open(this.url, '_blank');
  }
}
