# Evaluation Metrics

Following is a list of the metrics used to evaluate a game of chess between two Agents.

## Win Count
Number of Times a Player (White/Black) won.

    player_win_count = ∑ player_win(i)
    Where,
        i ∈ (0,total_match_count)

## Lose Count
Number of Times a Player (White/Black) won.
    
    player_lose_count = total_matche_count - player_win_count

## Draw Count
Number of Times the match ended with a draw.

    match_draw_count = ∑ outcome[i].match_draw,
    Where,
        i ∈ (0,total_match_count)

## Number of Turns
Total Number of Turns taken in the match.

## Number of Captures per Turn
Average number of turns needed for capturing pieces in a given match by a player.

    average_turns_per_capture = total_captures / total_turns

## Player Points
Total sum of points earned by capturing opponent pieces in a match by a player.

| Piece      | Capture Point |
|------------|---------------|
| Pawn (P)   | 1             |
| Rook (R)   | 3             |
| Bishop (B) | 3             |
| Knight (N) | 3             |
| Queen (Q)  | 9             |
| King (K)   | 20            |

## Player Points per Turn
Average points earned per turn by a player in a given match.
    
    average_points_per_turn = total_points/total_turns
