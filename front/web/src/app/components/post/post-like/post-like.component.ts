import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-post-like',
  templateUrl: './post-like.component.html',
  styleUrls: ['./post-like.component.css']
})
export class PostLikeComponent implements OnInit {
  @Input() likeCount: number;
  @Input() isLiked: boolean;
  @Output() likePost = new EventEmitter();

  constructor() { }

  ngOnInit() {
  }

  sendLike($event) {
    this.likePost.emit($event)
  }
}
