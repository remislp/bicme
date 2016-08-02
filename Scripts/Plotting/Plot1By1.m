function Plot1By1(fig,standardise,varargin)

% function Plot1By1(varargin)
%
% Shell function for plotting a figure with one set of axes.
% Consider altering the lines marked: ***
%
% INPUT
% optional: filename - name and location to export .eps file of
%           figure. Should not include the extension (e.g. no .eps
%           extension)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Settings

% Fonts
FontName = 'sans-serif';
FSsm = 12; %axis label font size
FSmed = 12;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set figure size

% PP = [0,0,2,2]; %*** paper position in inches
% PS = PP(end-1:end); % paper size in inches
% 
% set(figure1,'paperpositionmode','manual','paperposition', ...
%         PP,'papersize',PS, 'paperunits','inches');

if length(varargin)>0
  % So the figure is the same size on the screen as when it is printed:
  pu = get(fig,'PaperUnits');
  pp = get(fig,'PaperPosition');
  set(fig,'Units',pu,'Position',pp)
  left = 0.25; % space on LHS of figure
end

if length(varargin)>1
  % So the figure is the same size on the screen as when it is printed:
    FSsm = varargin{2}; %axis label font size
    FSmed = varargin{3};
    if length(varargin) >= 4
        %optional parameter for the left indent
        left = varargin{4};
    else
        left = 0.25; % space on LHS of figure
    end
    
    if length(varargin) == 5
        %optional parameter for figure size
        wh = varargin{5};
    else
        wh = [0,0,2,2]; 
    end
end

% set figure size
%fig = fig;

PP = wh; %*** paper position in inches
PS = PP(end-1:end); % paper size in inches

set(fig,'paperpositionmode','manual','paperposition', ...
         PP,'papersize',PS, 'paperunits','inches', 'position', PP);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Axis position

right = 0.1; % space on RHS of figure
top = 0.2; % space above figure
bottom = 0.25;% space below figure

height = (1-top-bottom); % height of axis
width = 1-left-right; % width of axis

pos1 = [left,1-top-height,width,height]; % position of axis

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plotting

AX=get(fig,'children');
if standardise
    for i=1:length(AX) %plotyy
        if isa(AX(i),'matlab.graphics.axis.Axes')
            
            set(AX(i),'position',pos1);
            hold on
            set(AX(i),'TickDir','out'); % alter the direction of the tick marks
            set(AX(i),'FontName',FontName,'FontSize',FSsm) % set the font name
                                                     % and size

            set(get(AX(i),'xlabel'),'FontSize',FSmed)
            set(get(AX(i),'ylabel'),'FontSize',FSmed)
            set(AX(i),'box','off') % turns the figure bounding box off
            set(AX(i),'layer','top') % tops problems with lines being plotted on
                       % top of the axis lines

            set(AX(i), 'XTickLabel', get(AX(i), 'XTick'), 'FontName','sans-serif');
            set(AX(i), 'YTickLabel', get(AX(i), 'YTick'), 'FontName','sans-serif');
            %set(AX(i),'LineWidth', 3)
                       
        elseif isa(AX(i),'matlab.graphics.illustration.Legend')
            set(AX(i),'box','off')
            set(AX(i),'LineWidth', 3)
        end
    end
else
    for i=1:length(AX)
        %keep the inset as is
        if isa(AX(i),'matlab.graphics.axis.Axes')
            set(AX(i),'position',pos1);
            hold on
            set(AX(i),'TickDir','out'); % alter the direction of the tick marks
            set(AX(i),'FontName',FontName,'FontSize',FSsm) % set the font name
                                                         % and size

            set(get(AX(i),'xlabel'),'FontSize',FSmed)
            set(get(AX(i),'ylabel'),'FontSize',FSmed) 
        elseif isa(AX(i),'matlab.graphics.illustration.Legend')
            set(AX(i),'box','off')
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%		       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Exporting

if length(varargin)>0 % if the user supplies a file name
  filename=[varargin{1},'.eps'];
  
  % choose the painters renderer, without cropping 
  print(fig, '-depsc', '-painters', filename,   '-loose','-r1200');
  
  % open the eps in ghostview
  %str = ['! gv ',filename,'&'];
  %eval(str)
end