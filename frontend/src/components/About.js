import React from 'react';
import styled from 'styled-components';
import websitePalette from '../styles/palette';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Title = styled.h1`
  font-size: clamp(2rem, 3vw, 40rem);
  margin-bottom: 20px;
  color: ${websitePalette.primary};
`;

const Bold = styled.span`
  font-weight: bold;
`;

function About() {

  return (
    <>
      <Container>
        <Title>Rules</Title>
        <h4>General information</h4>

        <p>
          Every challenge has a leaderboard. And so there's no exception to this one.
          There will be one total leaderboard, but also one for each type of activity* (*subject to grouping).
          The ranking in the total leaderboard is determined by the <Bold>Top 3 places of all activity based rankings</Bold> of a person.
          <br />
          Regarding points, a person comming in first in an activity ranking, will get 10 points. The tenth person in that ranking will get 1 point. You can guess the rest.
          <br />
          Imagine a person with a <Bold>first place in biking</Bold> a <Bold>fifth place in tennis</Bold> and a <Bold>third place in running</Bold>.
          Their total points will be: <Bold>10 (biking) + 6 (tennis) + 8 (running) = 24</Bold>.
          <br />
          In case there's a tie, the person with the higher value in overall moving time of all 3 categories wins the tiebreaker.
        </p>

        <h4>Accepted types of activities:</h4>

        <p>
          <Bold>Bike</Bold>: (Mountainbike, Virtualbike, Gravelbike)<br />
          <Bold>Run</Bold>: (Trailrun, Edgecase (Holleger Racewalk)<br />
          <Bold>Hiking</Bold>: (Skitour, Hiking, Schneeschuhwandern)<br />
          <Bold>Alpine Snow Sports</Bold>: (Ski, Snowboard)<br />
          <Bold>Langlaufen / Inline</Bold>: (selbsterklärend)<br />
          <Bold>Gym</Bold>: (Weighted Training, HIIT, Training)<br />
          <Bold>Ball Sports</Bold>: ( Volleyball, Football, Badminton, Pickleball, Tennis, Table Tennis, etc.)<br />
          <Bold>Klettern</Bold>: (Bouldern, Klettern)<br />
          <Bold>Water Sports</Bold>: (Canoe, Kayak, Kitesurf, Rowing, Stand Up Paddling, Surf, Swim, Windsurf)<br />
        </p>

        <h4>Prizepool</h4>

        <p>
          Each player has to deposit 10€ per month for the entire 12 months (for IBAN go to the WhatsApp Group).
          Depending on the amount of people participating in the challenge, the total amount of money gathered will be split into prizepool money and a smaller part for restaurant expenditures at the end of the year.
          The following example demonstrates earnings from the prizepool.
        </p>
        <p>
          example on 1000€:
          <br />
          1. 40% =&gt; 400<br />
          2. 25% =&gt; 250<br />
          3. 15% =&gt; 150<br />
          4. 11% =&gt; 110<br />
          5. 9% =&gt; 90<br />
        </p>
        <p>
          The first place will get 40% of the total prize money, followed with 25% for the second place and so on.
          This means that only the first five places will get extra money at all. However, there will still be a great evening at the end of the year at a restaurant, which will likely be paid by the prizepool money. So, everybody has some sort of benefit at the end.
        </p>
      </Container>
    </>
  );
}

export default About;