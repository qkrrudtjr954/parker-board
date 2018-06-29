import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PostLikeComponent } from './post-like.component';

describe('PostLikeComponent', () => {
  let component: PostLikeComponent;
  let fixture: ComponentFixture<PostLikeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PostLikeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PostLikeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
