Preregistered hypotheses about characters
=========================================

A set of 80 hypotheses we're using to confirm that the character-spaces extracted computationally from books bear some relation to human intuitions.

Some of these are drawn from twenty-nine hypotheses about nineteenth-century fiction used in Bamman et al. 2014. That original set has been enlarged, especially to cover twentieth-century fiction.

Each of the hypotheses affirms that a pair of characters should be more similar to each other than either of them is to a third character we call the "distractor." Each hypothesis thus defines two separate tests, since either (or both) of the characters in the original pair could violate the hypothesis by having a strong resemblance to the distractor.

We have defined the hypotheses to cover several different ways two characters might be understood as "similar."

1. First, instances of *the same character* who recur in different volumes of a series (e.g. Sherlock Holmes or Tarzan) obviously ought to resemble each other.

2. Secondly, *genres define recurring roles* that readers understand as structurally similar: the "detective," "murderer," or "victim" in a mystery, for instance. Different instances of those roles ought to resemble each other.

3. Third and finally, we can reason about characters as if they were real people, and frame hypotheses about various kinds of *social resemblance:* similarities in social position, profession, age, and gender. Since structural roles may not be strongly defined in realist novels, these naively realistic hypotheses are sometimes the only ones we can make about those works.

These forms of resemblance are likely to be complicated or obscured by several factors outside the story-world. The passage of *historical time* introduces lexical differences between books. *Authors* are also powerful conditioning factors: in a worst-case scenario, the family resemblances binding all the characters written by a single author might prevent a model from glimpsing moral and social connections between characters in different oeuvres.

Human beings are able to (partly) factor out formal and lexical factors when they reason about fictional characters, and we postulate that a good computational model of character will do the same thing. So our most ambitious hypotheses are designed to test a model's ability to recognize structural and social similarities between characters that belong to different oeuvres or periods.

We list hypotheses roughly from easy to hard, guided by the assumption that resemblance will be easiest to detect when several forms of resemblance align (comparing two male detectives written by the same author), and harder to detect when social categories are working against each other (does Miss Marple, written by Agatha Christie, resemble Nero Wolfe, written by Rex Stout? well, they're both detectives, but ...) We also acknowledge that human readers themselves may be doubtful about some of the more ambitious hypotheses listed here. We have tried to emphasize relatively clear forms of similarity, but we also wanted to toss in a few challenging/debatable questions, in order to make our models "stretch," and find out where they fail--even if those areas of "failure" turn out to be areas where human readers also disagree.

Instances of the same character, easy cases
--------------------------------------------

1. Sherlock Holmes, in *The Adventures of Sherlock Holmes,* resembles Holmes in *The Sign of Four* (Conan Doyle) more than either character resembles the brutal Bill Sikes in *Oliver Twist* (Dickens).

2. Sherlock Holmes, in *The Adventures of Sherlock Holmes,* resembles Holmes in *The Valley of Fear* (Conan Doyle) more than either character resembles Carrie Meeber in *Sister Carrie* (Dreiser).

3. Tarzan, in *Tarzan the Untamed,* resembles Tarzan in *Tarzan and the Jewels of Opar* (Burroughs) more than either resembles Rhett Butler in *Gone with the Wind* (Mitchell).

Instances of the same character, distractor from the same author
----------------------------------------------------------------

4. Sherlock Holmes, in *The Sign of Four,* resembles Holmes in *The Valley of Fear* (Conan Doyle) more than either resembles the murder victim John Douglas McMurdo in *The Valley of Fear* (Conan Doyle).

5. Tarzan, in *Tarzan the Untamed,* resembles Tarzan in *Tarzan and the Jewels of Opar* (Burroughs) more than either resembles the villain Werper in *Tarzan and the Jewels of Opar.*

6. Lord Peter Wimsey, in *The Nine Taylors,* resembles Peter Wimsey in *Strong Poison* (Sayers) more than either resembles Harriet Vane in *Strong Poison.*


Resemblances within the same author, distractor from outside
------------------------------------------------------------

7. Elizabeth Bennet in *Pride and Prejudice* resembles Elinor Dashwood in *Sense and Sensibility* (Austen) more than either character resembles King Richard in *Ivanhoe* (Scott). (Here and in the next example, the contrast should be especially easy because the comparands are linked by authorship, genre, and gender, and all those factors work against the distractor.)

8. Emily St. Aubert in *The Mysteries of Udolpho* resembles Adeline in *The Romance of the Forest* (both by Ann Radcliffe) more than either character resembles Uriah Heep in *David Copperfield* (Dickens).

9. Detective Hercule Poirot in *Thirteen at Dinner* resembles the detective Miss Marple in *The Mirror Crack'd from Side to Side* (both by Agatha Christie) more than either resembles Scarlett O'Hara in *Gone with the Wind* (Mitchell). The personalities of all three characters are different, but I assume that the conventional role "detective" will be the most powerful factor here, especially since it is reinforced by authorship.

10. Detective Hercule Poirot in *Thirteen at Dinner* resembles the detective Miss Marple in *The Mirror Crack'd from Side to Side* (both by Agatha Christie) more than either resembles the casino owner Eddie Mars, in *The Big Sleep* (Chandler).

11. Elizabeth Bennet in *Pride and Prejudice* resembles Elinor Dashwood in *Sense and Sensibility* (Austen) more than either character resembles Madame Merle in *Portrait of a Lady* (Henry James). (A version of hypothesis 7, but with gender now taken out of the equation.)

12. Wickham in *Pride and Prejudice* resembles Willoughby in *Sense and Sensibility* (Austen) more than either character resembles Mr Rochester in *Jane Eyre* (Brontë).

13. Lord Edgware, murder victim in *Thirteen at Dinner*, resembles Heather Badcock, murder victim in *The Mirror Crack'd* (both Agatha Christie) more than either resembles Jim Casy, former preacher in *The Grapes of Wrath* (Steinbeck).

14. Lady Edgware, murderer in *Thirteen at Dinner,* resembles Marina Gregg, murderer in *The Mirror Crack'd* (both Christie), more than either resembles Jennifer Cavilleri from *Love Story* (Erich Segal).

15. Diana “Die” Vernon in *Rob Roy* (Walter Scott) resembles Flora MacIvor in *Waverley* (Scott) more than she resembles Emily St. Aubert in The Mysteries of Udolpho (Radcliffe). (Diana and Flora are active characters surrounded by mystery; Emily St. Aubert is a largely passive point-of-view character.)

Resemblances within the same author, distractor from inside
-----------------------------------------------------------

16. Elizabeth Bennet in *Pride and Prejudice* resembles Elinor Dashwood in *Sense and Sensibility* (Austen) more than either character resembles Willoughby from *Sensibility*.

17. Emily St. Aubert in *The Mysteries of Udolpho* resembles Adeline in *The Romance of the Forest* (both by Ann Radcliffe) more than either character resembles Montoni from *Udolpho*.

18. Detective Hercule Poirot in *Thirteen at Dinner* resembles the detective Miss Marple in *The Mirror Crack'd from Side to Side* (both by Agatha Christie) more than either resembles the murderess Lady Edgware from *Thirteen at Dinner.*

19. Lord Edgware, murder victim in *Thirteen at Dinner*, resembles Heather Badcock, murder victim in *The Mirror Crack'd* (both Agatha Christie) more than either resembles Marina Gregg, the murderer in *The Mirror Crack'd*.

20. Lady Edgware, murderer in *Thirteen at Dinner,* resembles Marina Gregg, murderer in *The Mirror Crack'd* (both Christie), more than either resembles Hercule Poirot from *Thirteen at Dinner.*

21. Wickham in *Pride and Prejudice* (Jane Austen) resembles Willoughby in *Sense and Sensibility* more than either character resembles Mr Darcy in *Pride and Prejudice.* (Can we identify unreliable seducers?)

22. Elizabeth Bennet in *Pride and Prejudice* (Jane Austen) resembles Elinor Dashwood in *Sense and Sensibility* more than either character resembles Mrs Bennet in *Pride and Prejudice.* (Can we recognize thoughtful protagonists?)

23. John Barton, in *Mary Barton* (Elizabeth Gaskell) resembles Nicholas Higgins in *North and South* more than either character resembles Margaret Hale, in *North and South.* (Can we recognize honest workingmen?)

24. Agnes Wickfield in David Copperfield (Charles Dickens) resembles Lizzie Hexam in Our Mutual Friend more than either character resembles Uriah Heep in *Copperfield.* (Self-denying young women with troubled romantic histories.)

25. Rowena in *Ivanhoe* (Walter Scott) resembles Rose Bradwardine in *Waverley* more than she resembles Rebecca in *Ivanhoe.* (A debatable hypothesis, but this at least is Alexander Welsh’s argument about Scott’s “dark” and “light” heroines.)

26. Philippe, Marquis de Montalt in Ann Radcliffe’s *Romance of the Forest* resembles resembles Montoni in *The Mysteries of Udolpho* (Radcliffe) more than either character resembles Valancourt in *Udolpho.* (Gothic villains resemble each other more than they resemble the love interest.)

Structural resemblances across authors, distractor from outside
---------------------------------------------------------------

Genre fiction plays a big role here, because it tends to lean on clear structural patterns: e.g., there's usually a murderer, a murder victim, and a detective.

27. Gandalf, wizard in *The Return of the King* (Tolkien), resembles Merlyn, wizard in *The Sword in the Stone* (T. H. White), more than either resembles Ruthie Joad, reckless child from *The Grapes of Wrath* (Steinbeck).

28. Rhett Butler, devil-take-care love interest in *Gone with the Wind* (Mitchell), resembles Lord Damerel, devil-take-care love interest in *Venetia* (Heyer), more than either resembles Jim Casy, former preacher in *The Grapes of Wrath* (Steinbeck).

29. Scarlett O'Hara, protagonist of the historical romance *Gone with the Wind* (Mitchell), resembles Venetia, protagonist of the historical romance *Venetia* (Heyer), more than either resembles the detective Miss Marple from *The Mirror Crack'd* (Christie). (Is GWTW strictly a "romance"? Perhaps not. But it's closer to that than to a detective story.)

30. Jim Lassiter, enigmatic loner gunman in *Riders of the Purple Sage* (Zane Gray) resembles Shane, enigmatic loner gunman in *Shane* (Jack Schaefer), more than either resembles Lord Peter Wimsey in *Strong Poison* (Sayers).

31. Lord Mormont, aristocratic military leader in *Clash of Kings* (George R. R. Martin) resembles Faramir, aristocratic military leader in *Return of the King* (Tolkien), more than either resembles the drunkard Lucas Cross in *Peyton Place* (Metallious).

32. Hercule Poirot, detective in *Thirteen at Dinner* (Christie), resembles Sherlock Holmes in *The Valley of Fear* (Conan Doyle) more than either of them resemble Carmen Sternwood, bad girl murderer in *The Big Sleep* (Chandler).

33. Sherlock Holmes in *The Adventures of Sherlock Holmes* resembles Lord Peter Wimsey in *The Nine Tailors* more than either of them resemble Tom Joad, suffering working-class protagonist of *The Grapes of Wrath* (Steinbeck).

34. Detective Lord Peter Wimsey in *Strong Poison* (Sayers) resembles detective Miss Marple in *The Mirror Crack'd* (Christie) more than either of them resembles Jane Withersteen, heroic western woman in *Riders of the Purple Sage* (Zane Gray).

35. Miss Marple, detective in *The Mirror Crack'd* (Christie), resembles Nero Wolfe, armchair detective in *The Silent Speaker* (Rex Stout), more than either of them resemble Constance Mackenzie, the struggling protagonist of *Peyton Place* (Metallious).

36. Lord Edgware, the murder victim in *Thirteen at Dinner* (Christie), resembles Cheney Boone, the murder victim in *The Silent Speaker* (Stout), more than either resembles Tom Joad, suffering working-class protagonist of *The Grapes of Wrath* (Steinbeck).

37. John Douglas McMurdo, the murder victim in *The Valley of Fear* (Conan Doyle), resembles Philip Boyes, the murder victim in *Strong Poison* (Sayers), more than either of them resemble Elder Tull, the cowardly villain in *Riders of the Purple Sage* (Zane Gray).

38. Philip Boyes, killed by poison in *Strong Poison* (Sayers), resembles Heather Badcock, killed by poison in *The Mirror Crack'd* (Christie), more than either resembles Caroline Meeber, aspiring working-class protagonist of *Sister Carrie* (Dreiser).

39. Carmen Sternwood, glamorous murderer in *The Big Sleep* (Chandler), resembles Marina Gregg, glamorous murderer in *The Mirror Crack'd* (Christie), more than either resembles Merlyn in *The Sword in the Stone*.

40. Alger Kates, bookish murderer in *The Silent Speaker* (Stout), resembles Norman Urquhart, bookish murderer in *Strong Poison* (Sayers), more than either of them resemble Tarzan in *Tarzan the Untamed* (Burroughs).

41. Montoni in *Mysteries of Udolpho* (Radcliffe) resembles Heathcliff in *Wuthering Heights* (Emily Brontë) more than either character resembles Mr Bennet in *Pride and Prejudice.* (Montoni and Heathcliff are both cruel, proud, tormented figures who get called “Gothic” or “Byronic,” although Heathcliff is more sympathetic. Mr Bennet is nothing like them morally, but he is intermediate between them in time.)

Social resemblance across authors, distractor from outside
----------------------------------------------------------

The dividing line between "structural" and "social" resemblance is blurry; many cases involve both.

42. Arthur Donnithorne, in *Adam Bede* (George Eliot) resembles Alec d’Urberville in *Tess of the d’Urbervilles* (Thomas Hardy) more than either character resembles John Thornton in *North and South* (Elizabeth Gaskell). (The first two characters are aristocrats who seduce a young working-class woman; the third character is a mill-owner and a worthy suitor.)

43. Alice Humphreys, in *The Wide, Wide World* (Susan Warner) resembles Helen Burns in *Jane Eyre* (Charlotte Bronte) more than either character resembles Simon Legree in *Uncle Tom’s Cabin* (Harriet Beecher Stowe). (Spiritually-minded, sickly guide/helper figures resemble each other more than they resemble a brutal slaveowner.)

44. Bill Sikes in *Oliver Twist* (Dickens) resembles Long John Silver in *Treasure Island* (Stevenson) more than either character resembles Francisco in *The Pirate* (Frederick Marryat). Sikes and Silver are both villains, and Francisco is more or less the hero. But this is a relatively challenging test, because that characterological similarity is confounded by similarities of period (Dickens and Marryat are contemporary) and similarities of nautical setting (The Pirate / Treasure Island).

45. Tom Joad, struggling working-class protagonist of *The Grapes of Wrath* (Steinbeck), resembles Jurgis Rudkus, struggling working-class protagonist of *The Jungle* (Sinclair), more than either resembles Lord Henry from *Dorian Gray* (Wilde).

46. Ona Rudkus, exploited teenager in *The Jungle* (Sinclair), resembles Selena Cross, exploited teenager in *Peyton Place* (Metallious), more than either resembles Hercule Poirot.

47. Carrie Meeber, working-class (rising) protagonist of *Sister Carrie* (Dreiser), resembles Jurgis Rudkus, working-class protagonist of *The Jungle* (Sinclair), more than either resembles Tarzan, in *Tarzan the Untamed* (Burroughs).

48. Trilby, performer and tragic ingenue of *Trilby* (Du Maurier), resembles Sibyl Vane, performer and tragic ingenue of *Dorian Gray*, more than either resembles Madame Merle in *Portrait of a Lady* (James).

49. Dr. Matthew Swain, well-meaning doctor in *Peyton Place* (Metallious), resembles Dr. Neal, well-meaning doctor in *Good Luck, Miss Wyckhoff* (Inge), more than either resembles Alger Kates, the murderer in *The Silent Speaker* (Rex Stout).

Structural resemblances across authors, distractor from inside
--------------------------------------------------------------

Now we reach the really challenging task of recognizing that a character in author A may resemble a character in author B more than another character in A.

50. Jonathan Wild in *Jack Sheppard* (W. H. Ainsworth) resembles Bill Sikes in *Oliver Twist* (Dickens) more than either one resembles Mr. Brownlow in *Oliver Twist* (Dickens). The two Dickens characters may share some diction, but brutal murderers in the Newgate genre should resemble each other more than they resemble a philanthropist.

51. Isabel Archer, in *Portrait of a Lady* (Henry James) resembles Gwendolyn Harleth in *Daniel Deronda* (George Eliot) more than either character resembles Madame Merle in *Portrait.* (Both Isabel and Gwendolyn are independent spirits trapped in marriages to manipulative husbands. James is said to have drawn explicitly on Eliot’s novels (and perhaps specifically on Harleth) as models for Archer. Edel, Leon. *Henry James: The Conquest of London: 1870-1881.* Philadelphia and New York: J. B. Lippincott Company, 1962. However, no comparison involving James is going to be easy.)

52. Gilbert Osmond, in *Portrait of a Lady* (Henry James) resembles Henleigh Mallinger Grandcourt in *Daniel Deronda* (George Eliot) more than either character resembles Daniel Deronda in *Deronda.* (Our working hypothesis is that cruel, manipulative husbands resemble each other more than they resemble stand-up guys.)

53. Gandalf, wizard in *The Return of the King* (Tolkien), resembles Merlyn, wizard in *The Sword in the Stone* (T. H. White), more than either resembles Sauron, dark lord from *The Return of the King* (Tolkien).

54. Rhett Butler, devil-take-care love interest in *Gone with the Wind* (Mitchell), resembles Lord Damerel, devil-take-care love interest in *Venetia* (Heyer), more than either resembles Wade Hampton Hamilton, Scarlett's shy son by her first husband in *Gone with the Wind* (Mitchell).

55. Scarlett O'Hara, protagonist of the romance *Gone with the Wind* (Mitchell), resembles Venetia, protagonist of the romance *Venetia* (Heyer), more than either resembles the spinster Aunt Pittypat in *Gone with the Wind*.

56. Jim Lassiter, enigmatic loner gunman in *Riders of the Purple Sage* (Zane Gray) resembles Shane, enigmatic loner gunman in *Shane* (Jack Schaefer), more than either resembles the cowardly Elder Tull from *Purple Sage*.

57. Lord Mormont, aristocratic military leader in *Clash of Kings* (George R. R. Martin) resembles Faramir, aristocratic military leader in *Return of the King* (Tolkien), more than either resembles Sauron in *Return of the King*.

58. Hercule Poirot, detective in *Thirteen at Dinner* (Christie), resembles Sherlock Holmes in *The Valley of Fear* (Conan Doyle) more than either of them resemble Lord Edgware, the murder victim in *Thirteen at Dinner*.

59. Sherlock Holmes in *The Adventures of Sherlock Holmes* resembles his fellow detective Lord Peter Wimsey in *The Nine Tailors* more than either of them resemble William Thoday, the (or *a*) murderer in *Nine Tailors*.

60. Detective Lord Peter Wimsey in *Strong Poison* (Sayers) resembles detective Miss Marple in *The Mirror Crack'd* (Christie) more than either of them resembles Marina Gregg, the murderer in *The Mirror Crack'd*.

61. Miss Marple, detective in *The Mirror Crack'd* (Christie), resembles Nero Wolfe, armchair detective in *The Silent Speaker* (Rex Stout), more than either of them resemble Cheney Boone, the murder victim in *Silent Speaker*.

62. (Reaching across a good bit of time) Sherlock Holmes, from *The Adventures of Sherlock Holmes,* resembles Nero Wolfe in *The Silent Speaker* more than either of them resemble Alger Kates, the murderer in *Silent Speaker*.

63. Lord Edgware, the murder victim in *Thirteen at Dinner* (Christie), resembles Cheney Boone, the murder victim in *The Silent Speaker* (Stout), more than either resembles Lady Edgware, the murderer in *Thirteen at Dinner*.

64. John Douglas McMurdo, the murder victim in *The Valley of Fear* (Conan Doyle), resembles Philip Boyes, the murder victim in *Strong Poison* (Sayers), more than either of them resemble the mystery writer Harriet Vane in *Strong Poison*.

65. Alger Kates, bookish murderer in *The Silent Speaker* (Stout), resembles Norman Urquhart, bookish murderer in *Strong Poison* (Sayers), more than either of them resemble Nero Wolfe, the detective in *Silent Speaker*.

66. Carmen Sternwood, glamorous murderer in *The Big Sleep* (Chandler), resembles Marina Gregg, glamorous murderer in *The Mirror Crack'd* (Christie), more than either resembles Miss Marple, the detective in *Mirror Crack'd*.

Social resemblance across authors, distractor from inside
----------------------------------------------------------

These hypotheses start to get pretty weak, because we can't be confident that social similarity *ought* to trump genre and authorial style. I have accordingly not created many of them.

67. Tom Joad, struggling working-class protagonist of *The Grapes of Wrath* (Steinbeck), resembles Jurgis Rudkus, struggling working-class protagonist of *The Jungle* (Sinclair), more than either resembles Durham, a factory owner in *The Jungle*.

68. Ona Rudkus, exploited teenager in *The Jungle* (Sinclair), resembles Selena Cross, exploited teenager in *Peyton Place* (Metallious), more than either resembles Constance Mackenzie, worried mother in *Peyton Place.*

69. Trilby, performer and tragic ingenue of *Trilby* (Du Maurier), resembles *Sibyl Vane*, performer and tragic ingenue of *Dorian Gray*, more than either resembles Lord Henry, cynical aristocrat in *Dorian Gray.*

70. Dr. Matthew Swain, well-meaning doctor in *Peyton Place* (Metallious), resembles Dr. Neal, well-meaning doctor in *Good Luck, Miss Wyckhoff* (Inge), more than either resembles Lucas Cross, abusive drunkard from *Peyton Place*.

71. Contrasts of age. Wade Hampton Hamilton, Scarlett's son in *Gone with the Wind,* resembles Ruthie Joad, a reckless child in *Grapes of Wrath*, more than either resembles the spinster Aunt Pittypat in *Gone with the Wind.*

72. Tom Sawyer, in *The Adventures of Tom Sawyer* should resemble Oliver in *Oliver Twist* more than either character resembles Miss Havisham in *Great Expectations.* Contrast of age, but this is a debatable hypothesis because Tom often speaks in a national/provincial dialect.

73. Mr. Darcy in *Pride and Prejudice* should resemble Edward Waverly in *Waverly* (Walter Scott) more than either character resembles the villain Rashleigh Osbaldistone in *Rob Roy.* Moral contrast.


Hypotheses that are weak because disrupted by a lot of historical time
-----------------------------------------------------------------------

Comparisons that cross more than 50 years may be difficult. Indeed, human readers may not agree about some of these. One could contend that differences of genre and history *should* trump naively realistic social comparisons. It nevertheless seems worthwhile to construct a few risky hypotheses, in order to test the model's ability to weigh social and formal factors against each other. I hardly dare to expect that distractors from the same author can be resisted across this distance, but have ventured a few to give the model something to reach for. Otherwise, I've gone for distractors located at an intermediate point on the timeline.

74. Silas Ruthyn, in *Uncle Silas* (Sheridan LeFanu) resembles Montoni in *The Mysteries of Udolpho* (Ann Radcliffe) more than either character resembles Valancourt in *Udolpho.* (Gothic villains who play a similar role in the plot, but are located a century from each other.)

75. Elizabeth Bennet, from *Pride and Prejudice,* resembles the Regency romance heroine Venetia in *Venetia* (Heyer) more than either character resembles Wickham in *P&P*. This is a very debatable hypothesis; romances in the Regency are not the same thing as Regency romances, and the heroines have different temperaments.

76. Huck Finn in *The Adventures of Tom Sawyer* resembles Ruthie Joad, reckless kid in *The Grapes of Wrath*, more than either of them resemble the older cynical aristocrat Lord Henry in *Dorian Gray*. Fundamentally this is a question about similarities and differences of age.

77. Bill Sikes, brutal abuser of children in *Oliver Twist* (Dickens) resembles Lucas Cross, brutal abuser of children in *Peyton Place* (Metallious), more than either of them resemble Daniel Deronda in *Deronda* (Eliot).

78. Jennifer Cavilleri, female lead of *Love Story* (Erich Segal) resembles Elinor Dashwood, female lead of *Sense and Sensibility* (Austen), more than either of them resemble the murderess Carmen Sternwood from *Big Sleep* (Chandler). This is a very, very loose structural similarity: Segal is not a lot like Austen.

79. Faramir, noble military leader in *Return of the King* (Tolkien), resembles King Richard, noble military leader in *Ivanhoe* (Scott) more than either resembles Elder Tull, the cowardly villain in *Riders of the Purple Sage*.

80. The working-class labor organizer Nicholas Higgins, in *North and South* (Gaskell) should resemble the working-class labor organizer Jim Casy, in *The Grapes of Wrath* (Steinbeck) more than either resembles Lord Peter Wimsey in *Strong Poison*.
