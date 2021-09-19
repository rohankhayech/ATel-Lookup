import {
  ComponentFactory,
  ComponentFactoryResolver,
  ComponentRef,
  Directive,
  HostListener,
  Input,
  ViewContainerRef,
} from '@angular/core';
import {
  MatProgressBar,
  ProgressBarMode,
} from '@angular/material/progress-bar';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';

@Directive({
  selector: '[appProgressBar]',
})
export class ProgressBarDirective {
  @Input() public appProgressBar!: () => Observable<unknown>;
  @Input() public appProgressBarMode?: ProgressBarMode;

  private componentFactory: ComponentFactory<MatProgressBar>;
  private component?: ComponentRef<MatProgressBar>;

  constructor(
    private viewContainerRef: ViewContainerRef,
    componentFactoryResolver: ComponentFactoryResolver
  ) {
    this.componentFactory =
      componentFactoryResolver.resolveComponentFactory(MatProgressBar);
  }

  @HostListener('click') onMouseLeave() {
    this.createProgressBar();
    this.appProgressBar()
      .pipe(finalize(() => this.destroyProgressBar()))
      .subscribe();
  }

  createProgressBar() {
    this.component = this.viewContainerRef.createComponent<MatProgressBar>(
      this.componentFactory
    );
    this.component.instance.mode = this.appProgressBarMode ?? 'indeterminate';
    this.component.instance.color = 'accent';
  }

  destroyProgressBar() {
    this.component?.destroy();
  }
}
