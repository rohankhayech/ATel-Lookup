import { Component } from '@angular/core';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-authenticate-page',
  templateUrl: './authenticate-page.component.html',
  styleUrls: ['./authenticate-page.component.scss'],
})
export class AuthenticatePageComponent {
  public username = '';
  public password = '';

  constructor(private authenticationService: AuthenticationService) {}

  authenticate() {
    this.authenticationService
      .authenticate(this.username, this.password)
      .subscribe();
  }
}
