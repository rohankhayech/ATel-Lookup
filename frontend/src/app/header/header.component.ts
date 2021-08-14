import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  public label: string;

  constructor(private authenticationService: AuthenticationService) {
    this.label =
      this.authenticationService.token !== null
        ? 'Admin Portal'
        : 'Admin Login';
  }

  ngOnInit(): void {}
}
