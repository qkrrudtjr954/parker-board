import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import {Board, NavBoard} from "../../../models/board";
import {Router} from "@angular/router";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-navbar',
  template: `
    <nav class="col-md-2 d-none d-md-block bg-light sidebar">
      <div class="d-flex justify-content-center">
        <a class="btn btn-primary" routerLink="/boards/create">Board 생성하기</a>
      </div>
      <div class="sidebar-sticky">
        <ul class="nav flex-column">
          <li class="nav-item" *ngFor="let board of boardList">
            <div class="nav-link" [class.active]="board === selectedBoard">
              <a (click)="onSelected(board)" routerLink="/boards/{{board.id}}/posts">{{board.title}}</a>
            </div>
          </li>
        </ul>
      </div>
    </nav>

  `,
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  boardList: NavBoard[] = [];
  selectedBoard: NavBoard;

  constructor(private boardService: BoardService,
              private authService: AuthService,
              private router: Router) { }

  getNavBoardList() {
    this.boardService.getNavBoardList()
      .subscribe((data: NavBoard[]) => {
        this.boardList = data;
      })
  }

  onSelected(board: Board) {
    this.selectedBoard = board;
    this.router.navigate([`/boards/${board.id}/posts`])
  }

  ngOnInit() {
    this.getNavBoardList();
  }
}
