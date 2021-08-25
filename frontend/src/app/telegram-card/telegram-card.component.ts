import { Component, Input, OnInit } from '@angular/core';
import { Telegram } from '../telegram.interface';

@Component({
  selector: 'app-telegram-card',
  templateUrl: './telegram-card.component.html',
  styleUrls: ['./telegram-card.component.scss'],
})
export class TelegramCardComponent implements OnInit {
  @Input() public telegram?: Telegram;

  constructor() {}

  ngOnInit(): void {}
}
