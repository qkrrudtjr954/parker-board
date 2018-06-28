import { Component, OnInit } from '@angular/core';
import {Input} from "@angular/core";
import {BoardService} from "../../../services/board.service";
import {Board} from "../../../models/board";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-board-detail',
  templateUrl: './board-detail.component.html',
  styleUrls: ['./board-detail.component.css']
})
export class BoardDetailComponent implements OnInit {
  @Input() boardId: number;
  board: Board;
  isOwner: boolean = false;

  constructor(private boardService: BoardService,
              private authService: AuthService) { }

  ngOnInit() {
    this.getBoard();
  }

  getBoard(){
    this.boardService.getBoard(this.boardId)
      .subscribe((data: Board) => {
        this.board = data;
        this.isOwner = this.authService.isOwner(data.user.email)
      });
  }


}
