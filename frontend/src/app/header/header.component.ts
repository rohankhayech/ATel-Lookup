import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  public authenticated = false;

  constructor(
    private authenticationService: AuthenticationService,
    private router: Router
  ) {
    this.authenticationService.token$.subscribe((token) => {
      this.authenticated = token !== null;
    });
  }

  invalidate() {
    this.authenticationService.invalidate();

    this.router.navigate(['/']);
  }
}
