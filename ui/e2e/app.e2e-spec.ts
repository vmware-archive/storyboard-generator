import { StoryboardPage } from './app.po';

describe('storyboard App', () => {
  let page: StoryboardPage;

  beforeEach(() => {
    page = new StoryboardPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
