import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminPageComponent } from './admin-page/admin-page.component';
import { AuthenticatePageComponent } from './authenticate-page/authenticate-page.component';
import { AuthenticatedGuard } from './authenticated.guard';
import { HomePageComponent } from './home-page/home-page.component';
import { UnauthenticatedGuard } from './unauthenticated.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    component: HomePageComponent,
  },
  {
    path: '',
    canActivateChild: [UnauthenticatedGuard],
    children: [
      {
        path: 'authenticate',
        component: AuthenticatePageComponent,
      },
    ],
  },
  {
    path: '',
    canActivateChild: [AuthenticatedGuard],
    children: [
      {
        path: 'admin',
        component: AdminPageComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
