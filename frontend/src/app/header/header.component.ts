import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  public icon?: string;

  constructor(private authenticationService: AuthenticationService) {
    this.authenticationService.token$.subscribe((token) => {
      this.icon = token !== null ? 'admin_panel_settings' : 'login';
    });
  }

  ngOnInit(): void {}
}
