Sixteen new hypotheses to acknowledge in-book similarity
=======================================================

Because it seemed obvious that characters in the same book would resemble each other, my initial list of 92 hypotheses tended to emphasize harder tests, especially cases where two characters in different books ought to resemble *each other* more than either resembles a third character from one of the two books.

It's good that I looked for hard tests. But it also creates a potential blind spot, because the best-performing model I have found tends to separate in-book similarity from other forms of similarity. I need to make sure that its high performance isn't an accidental consequence of having a lot of hypotheses where an in-book similarity is *expected* to be weaker than a cross-book comparison. There are forty such comparisons in the existing list, and only two where in-book similarity is expected to be stronger than cross-book.

To even the scales a bit, I've framed sixteen new hypotheses where in-book similarities are expected to be strong. Since each hypothesis produces two distinct comparisons, this will add up to thirty-two comparisons where cross-book similarity is expected to be weaker than in-book. These hypotheses are mostly going to look mind-numbingly obvious. That's the idea! I'm trying to make sure that my model isn't succeeding by ignoring or minimizing the obvious fact of in-book similarity.

93. Merry and Pippin, in Tolkien's *Return of the King,* resemble each other more than they resemble Sauron, from the same book.

94. Merry and Pippin, in *Return of the King,* resemble each other more than they resemble Hugo Belfounder, from *Under the Net*, written by Iris Murdoch around the same time.

95. Tom Joad and Al Joad, brothers in Steinbeck's *Grapes of Wrath*, resemble each other more than either resembles Lady Edgware, the murderer in Christie's *Thirteen at Dinner*.

96. Tom Joad and Al Joad, brothers in Steinbeck's *Grapes of Wrath*, resemble each other more than either resembles the painter Basil Hallward, in Oscar Wilde's *Dorian Gray*.

97. Al Joad and Ruthie Joad, siblings in Steinbeck's *Grapes of Wrath*, resemble each other more than either resembles the detective Nero Wolfe, in *The Silent Speaker.*

98. Al Joad and Ruthie Joad, siblings in Steinbeck's *Grapes of Wrath*, resemble each other more than either resembles Lord Rotherham, in *Bath Tangle*, by Georgette Heyer. Differences of age and class as well as genre. 

99. Iza and Ayla, two Paleolithic women in Jean Auel's *Clan of the Cave Bear*, resemble each other more than either resembles Kezia St Martin, a journalist and romantic lead in Danielle Steele's *Passion's Promise.*

100. Iza, in *Clan of the Cave Bear*, resembles Brun, a fellow Neanderthal, more than either resembles Rick Deckard in *Do Androids Dream of Electric Sheep.*

101. Iza, in *Clan of the Cave Bear*, resembles Brun, a fellow Neanderthal, more than either resembles the detective Miss Marple in Agatha Christie's *The Mirror Crack'd*.

102. Wilfred of Ivanhoe resembles King Richard, in *Ivanhoe*, more than either character resembles Bill Sikes, from *Oliver Twist*.

103. Wilfred of Ivanhoe resembles King Richard, in *Ivanhoe*, more than either character resembles Isabel Archer, in *Portrait of a Lady* (James).

104. In *Ivanhoe*, Rowena resembles Rebecca more than either resembles Mr Rochester, in *Jane Eyre*. (Obvious similarities of period, genre, and gender, plus Rochester's very different function in the plot.)

105. In Chester Himes' *Blind Man with a Pistol*, Grave Digger Jones resembles his partner "Coffin" Ed Johnson more than either character resembles Dr. Neal in Inge, *Good Luck, Miss Wyckhoff.*

106. In Chester Himes' *Blind Man with a Pistol*, Grave Digger Jones resembles his partner "Coffin" Ed Johnson more than either character resembles Jennifer Cavilleri from *Love Story* (Erich Segal).

107. In Danielle Steele's *Passion's Promise,* the protagonist Kezia St Martin resembles her love interest Lucas Johns more than either of them resemble Theon Greyjoy from George R. R. Martin's *Clash of Kings*.

108. In E. M. Forster's *Howard's End*, Margaret Schlegel resembles her sister Helen more than either of them resemble the brittle murderer Carmen Sternwood, from *The Big Sleep*.

